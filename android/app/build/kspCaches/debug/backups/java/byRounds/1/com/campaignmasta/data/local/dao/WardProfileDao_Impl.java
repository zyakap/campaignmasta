package com.campaignmasta.data.local.dao;

import android.database.Cursor;
import android.os.CancellationSignal;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.room.CoroutinesRoom;
import androidx.room.EntityInsertionAdapter;
import androidx.room.RoomDatabase;
import androidx.room.RoomSQLiteQuery;
import androidx.room.SharedSQLiteStatement;
import androidx.room.util.CursorUtil;
import androidx.room.util.DBUtil;
import androidx.sqlite.db.SupportSQLiteStatement;
import com.campaignmasta.data.local.entity.WardProfileEntity;
import java.lang.Class;
import java.lang.Exception;
import java.lang.Integer;
import java.lang.Object;
import java.lang.Override;
import java.lang.String;
import java.lang.SuppressWarnings;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.Callable;
import javax.annotation.processing.Generated;
import kotlin.Unit;
import kotlin.coroutines.Continuation;
import kotlinx.coroutines.flow.Flow;

@Generated("androidx.room.RoomProcessor")
@SuppressWarnings({"unchecked", "deprecation"})
public final class WardProfileDao_Impl implements WardProfileDao {
  private final RoomDatabase __db;

  private final EntityInsertionAdapter<WardProfileEntity> __insertionAdapterOfWardProfileEntity;

  private final SharedSQLiteStatement __preparedStmtOfDeleteAll;

  public WardProfileDao_Impl(@NonNull final RoomDatabase __db) {
    this.__db = __db;
    this.__insertionAdapterOfWardProfileEntity = new EntityInsertionAdapter<WardProfileEntity>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "INSERT OR REPLACE INTO `ward_profiles` (`localId`,`serverId`,`wardId`,`wardName`,`wardNumber`,`llgName`,`councillorName`,`supportStrength`,`populationEstimate`,`estimatedVotingPopulation`,`keyClans`,`keyChurches`,`mainCommunityIssues`,`notesForCandidate`,`securityConcerns`,`updatedAt`) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement,
          @NonNull final WardProfileEntity entity) {
        statement.bindString(1, entity.getLocalId());
        statement.bindLong(2, entity.getServerId());
        statement.bindLong(3, entity.getWardId());
        statement.bindString(4, entity.getWardName());
        statement.bindString(5, entity.getWardNumber());
        statement.bindString(6, entity.getLlgName());
        statement.bindString(7, entity.getCouncillorName());
        statement.bindString(8, entity.getSupportStrength());
        if (entity.getPopulationEstimate() == null) {
          statement.bindNull(9);
        } else {
          statement.bindLong(9, entity.getPopulationEstimate());
        }
        if (entity.getEstimatedVotingPopulation() == null) {
          statement.bindNull(10);
        } else {
          statement.bindLong(10, entity.getEstimatedVotingPopulation());
        }
        statement.bindString(11, entity.getKeyClans());
        statement.bindString(12, entity.getKeyChurches());
        statement.bindString(13, entity.getMainCommunityIssues());
        statement.bindString(14, entity.getNotesForCandidate());
        statement.bindString(15, entity.getSecurityConcerns());
        statement.bindString(16, entity.getUpdatedAt());
      }
    };
    this.__preparedStmtOfDeleteAll = new SharedSQLiteStatement(__db) {
      @Override
      @NonNull
      public String createQuery() {
        final String _query = "DELETE FROM ward_profiles";
        return _query;
      }
    };
  }

  @Override
  public Object insertAll(final List<WardProfileEntity> entities,
      final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        __db.beginTransaction();
        try {
          __insertionAdapterOfWardProfileEntity.insert(entities);
          __db.setTransactionSuccessful();
          return Unit.INSTANCE;
        } finally {
          __db.endTransaction();
        }
      }
    }, $completion);
  }

  @Override
  public Object deleteAll(final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        final SupportSQLiteStatement _stmt = __preparedStmtOfDeleteAll.acquire();
        try {
          __db.beginTransaction();
          try {
            _stmt.executeUpdateDelete();
            __db.setTransactionSuccessful();
            return Unit.INSTANCE;
          } finally {
            __db.endTransaction();
          }
        } finally {
          __preparedStmtOfDeleteAll.release(_stmt);
        }
      }
    }, $completion);
  }

  @Override
  public Flow<List<WardProfileEntity>> getAllFlow() {
    final String _sql = "SELECT * FROM ward_profiles ORDER BY wardName ASC";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    return CoroutinesRoom.createFlow(__db, false, new String[] {"ward_profiles"}, new Callable<List<WardProfileEntity>>() {
      @Override
      @NonNull
      public List<WardProfileEntity> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfLocalId = CursorUtil.getColumnIndexOrThrow(_cursor, "localId");
          final int _cursorIndexOfServerId = CursorUtil.getColumnIndexOrThrow(_cursor, "serverId");
          final int _cursorIndexOfWardId = CursorUtil.getColumnIndexOrThrow(_cursor, "wardId");
          final int _cursorIndexOfWardName = CursorUtil.getColumnIndexOrThrow(_cursor, "wardName");
          final int _cursorIndexOfWardNumber = CursorUtil.getColumnIndexOrThrow(_cursor, "wardNumber");
          final int _cursorIndexOfLlgName = CursorUtil.getColumnIndexOrThrow(_cursor, "llgName");
          final int _cursorIndexOfCouncillorName = CursorUtil.getColumnIndexOrThrow(_cursor, "councillorName");
          final int _cursorIndexOfSupportStrength = CursorUtil.getColumnIndexOrThrow(_cursor, "supportStrength");
          final int _cursorIndexOfPopulationEstimate = CursorUtil.getColumnIndexOrThrow(_cursor, "populationEstimate");
          final int _cursorIndexOfEstimatedVotingPopulation = CursorUtil.getColumnIndexOrThrow(_cursor, "estimatedVotingPopulation");
          final int _cursorIndexOfKeyClans = CursorUtil.getColumnIndexOrThrow(_cursor, "keyClans");
          final int _cursorIndexOfKeyChurches = CursorUtil.getColumnIndexOrThrow(_cursor, "keyChurches");
          final int _cursorIndexOfMainCommunityIssues = CursorUtil.getColumnIndexOrThrow(_cursor, "mainCommunityIssues");
          final int _cursorIndexOfNotesForCandidate = CursorUtil.getColumnIndexOrThrow(_cursor, "notesForCandidate");
          final int _cursorIndexOfSecurityConcerns = CursorUtil.getColumnIndexOrThrow(_cursor, "securityConcerns");
          final int _cursorIndexOfUpdatedAt = CursorUtil.getColumnIndexOrThrow(_cursor, "updatedAt");
          final List<WardProfileEntity> _result = new ArrayList<WardProfileEntity>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final WardProfileEntity _item;
            final String _tmpLocalId;
            _tmpLocalId = _cursor.getString(_cursorIndexOfLocalId);
            final int _tmpServerId;
            _tmpServerId = _cursor.getInt(_cursorIndexOfServerId);
            final int _tmpWardId;
            _tmpWardId = _cursor.getInt(_cursorIndexOfWardId);
            final String _tmpWardName;
            _tmpWardName = _cursor.getString(_cursorIndexOfWardName);
            final String _tmpWardNumber;
            _tmpWardNumber = _cursor.getString(_cursorIndexOfWardNumber);
            final String _tmpLlgName;
            _tmpLlgName = _cursor.getString(_cursorIndexOfLlgName);
            final String _tmpCouncillorName;
            _tmpCouncillorName = _cursor.getString(_cursorIndexOfCouncillorName);
            final String _tmpSupportStrength;
            _tmpSupportStrength = _cursor.getString(_cursorIndexOfSupportStrength);
            final Integer _tmpPopulationEstimate;
            if (_cursor.isNull(_cursorIndexOfPopulationEstimate)) {
              _tmpPopulationEstimate = null;
            } else {
              _tmpPopulationEstimate = _cursor.getInt(_cursorIndexOfPopulationEstimate);
            }
            final Integer _tmpEstimatedVotingPopulation;
            if (_cursor.isNull(_cursorIndexOfEstimatedVotingPopulation)) {
              _tmpEstimatedVotingPopulation = null;
            } else {
              _tmpEstimatedVotingPopulation = _cursor.getInt(_cursorIndexOfEstimatedVotingPopulation);
            }
            final String _tmpKeyClans;
            _tmpKeyClans = _cursor.getString(_cursorIndexOfKeyClans);
            final String _tmpKeyChurches;
            _tmpKeyChurches = _cursor.getString(_cursorIndexOfKeyChurches);
            final String _tmpMainCommunityIssues;
            _tmpMainCommunityIssues = _cursor.getString(_cursorIndexOfMainCommunityIssues);
            final String _tmpNotesForCandidate;
            _tmpNotesForCandidate = _cursor.getString(_cursorIndexOfNotesForCandidate);
            final String _tmpSecurityConcerns;
            _tmpSecurityConcerns = _cursor.getString(_cursorIndexOfSecurityConcerns);
            final String _tmpUpdatedAt;
            _tmpUpdatedAt = _cursor.getString(_cursorIndexOfUpdatedAt);
            _item = new WardProfileEntity(_tmpLocalId,_tmpServerId,_tmpWardId,_tmpWardName,_tmpWardNumber,_tmpLlgName,_tmpCouncillorName,_tmpSupportStrength,_tmpPopulationEstimate,_tmpEstimatedVotingPopulation,_tmpKeyClans,_tmpKeyChurches,_tmpMainCommunityIssues,_tmpNotesForCandidate,_tmpSecurityConcerns,_tmpUpdatedAt);
            _result.add(_item);
          }
          return _result;
        } finally {
          _cursor.close();
        }
      }

      @Override
      protected void finalize() {
        _statement.release();
      }
    });
  }

  @Override
  public Object getByLocalId(final String localId,
      final Continuation<? super WardProfileEntity> $completion) {
    final String _sql = "SELECT * FROM ward_profiles WHERE localId = ?";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 1);
    int _argIndex = 1;
    _statement.bindString(_argIndex, localId);
    final CancellationSignal _cancellationSignal = DBUtil.createCancellationSignal();
    return CoroutinesRoom.execute(__db, false, _cancellationSignal, new Callable<WardProfileEntity>() {
      @Override
      @Nullable
      public WardProfileEntity call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfLocalId = CursorUtil.getColumnIndexOrThrow(_cursor, "localId");
          final int _cursorIndexOfServerId = CursorUtil.getColumnIndexOrThrow(_cursor, "serverId");
          final int _cursorIndexOfWardId = CursorUtil.getColumnIndexOrThrow(_cursor, "wardId");
          final int _cursorIndexOfWardName = CursorUtil.getColumnIndexOrThrow(_cursor, "wardName");
          final int _cursorIndexOfWardNumber = CursorUtil.getColumnIndexOrThrow(_cursor, "wardNumber");
          final int _cursorIndexOfLlgName = CursorUtil.getColumnIndexOrThrow(_cursor, "llgName");
          final int _cursorIndexOfCouncillorName = CursorUtil.getColumnIndexOrThrow(_cursor, "councillorName");
          final int _cursorIndexOfSupportStrength = CursorUtil.getColumnIndexOrThrow(_cursor, "supportStrength");
          final int _cursorIndexOfPopulationEstimate = CursorUtil.getColumnIndexOrThrow(_cursor, "populationEstimate");
          final int _cursorIndexOfEstimatedVotingPopulation = CursorUtil.getColumnIndexOrThrow(_cursor, "estimatedVotingPopulation");
          final int _cursorIndexOfKeyClans = CursorUtil.getColumnIndexOrThrow(_cursor, "keyClans");
          final int _cursorIndexOfKeyChurches = CursorUtil.getColumnIndexOrThrow(_cursor, "keyChurches");
          final int _cursorIndexOfMainCommunityIssues = CursorUtil.getColumnIndexOrThrow(_cursor, "mainCommunityIssues");
          final int _cursorIndexOfNotesForCandidate = CursorUtil.getColumnIndexOrThrow(_cursor, "notesForCandidate");
          final int _cursorIndexOfSecurityConcerns = CursorUtil.getColumnIndexOrThrow(_cursor, "securityConcerns");
          final int _cursorIndexOfUpdatedAt = CursorUtil.getColumnIndexOrThrow(_cursor, "updatedAt");
          final WardProfileEntity _result;
          if (_cursor.moveToFirst()) {
            final String _tmpLocalId;
            _tmpLocalId = _cursor.getString(_cursorIndexOfLocalId);
            final int _tmpServerId;
            _tmpServerId = _cursor.getInt(_cursorIndexOfServerId);
            final int _tmpWardId;
            _tmpWardId = _cursor.getInt(_cursorIndexOfWardId);
            final String _tmpWardName;
            _tmpWardName = _cursor.getString(_cursorIndexOfWardName);
            final String _tmpWardNumber;
            _tmpWardNumber = _cursor.getString(_cursorIndexOfWardNumber);
            final String _tmpLlgName;
            _tmpLlgName = _cursor.getString(_cursorIndexOfLlgName);
            final String _tmpCouncillorName;
            _tmpCouncillorName = _cursor.getString(_cursorIndexOfCouncillorName);
            final String _tmpSupportStrength;
            _tmpSupportStrength = _cursor.getString(_cursorIndexOfSupportStrength);
            final Integer _tmpPopulationEstimate;
            if (_cursor.isNull(_cursorIndexOfPopulationEstimate)) {
              _tmpPopulationEstimate = null;
            } else {
              _tmpPopulationEstimate = _cursor.getInt(_cursorIndexOfPopulationEstimate);
            }
            final Integer _tmpEstimatedVotingPopulation;
            if (_cursor.isNull(_cursorIndexOfEstimatedVotingPopulation)) {
              _tmpEstimatedVotingPopulation = null;
            } else {
              _tmpEstimatedVotingPopulation = _cursor.getInt(_cursorIndexOfEstimatedVotingPopulation);
            }
            final String _tmpKeyClans;
            _tmpKeyClans = _cursor.getString(_cursorIndexOfKeyClans);
            final String _tmpKeyChurches;
            _tmpKeyChurches = _cursor.getString(_cursorIndexOfKeyChurches);
            final String _tmpMainCommunityIssues;
            _tmpMainCommunityIssues = _cursor.getString(_cursorIndexOfMainCommunityIssues);
            final String _tmpNotesForCandidate;
            _tmpNotesForCandidate = _cursor.getString(_cursorIndexOfNotesForCandidate);
            final String _tmpSecurityConcerns;
            _tmpSecurityConcerns = _cursor.getString(_cursorIndexOfSecurityConcerns);
            final String _tmpUpdatedAt;
            _tmpUpdatedAt = _cursor.getString(_cursorIndexOfUpdatedAt);
            _result = new WardProfileEntity(_tmpLocalId,_tmpServerId,_tmpWardId,_tmpWardName,_tmpWardNumber,_tmpLlgName,_tmpCouncillorName,_tmpSupportStrength,_tmpPopulationEstimate,_tmpEstimatedVotingPopulation,_tmpKeyClans,_tmpKeyChurches,_tmpMainCommunityIssues,_tmpNotesForCandidate,_tmpSecurityConcerns,_tmpUpdatedAt);
          } else {
            _result = null;
          }
          return _result;
        } finally {
          _cursor.close();
          _statement.release();
        }
      }
    }, $completion);
  }

  @NonNull
  public static List<Class<?>> getRequiredConverters() {
    return Collections.emptyList();
  }
}
